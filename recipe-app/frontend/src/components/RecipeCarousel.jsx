import { useCallback, useEffect, useRef, useState } from "react";
import { Link } from "react-router";
import { formatTime } from "../utils/formatTime";

// Horizontal distance between card centers, in px
const CARD_SPACING = 260;
// How much of the velocity survives each 16ms frame of free spinning
const FRICTION = 0.94;
// Below this speed (cards/ms) the carousel stops coasting and snaps to a card
const SNAP_SPEED = 0.002;
// Spring stiffness used when snapping to the nearest card
const SNAP_STIFFNESS = 0.15;
// Pointer movement (px) before a press counts as a drag rather than a click
const DRAG_THRESHOLD = 6;
// Converts wheel/trackpad delta (px) into velocity (cards/ms)
const WHEEL_FACTOR = 0.00006;

export default function RecipeCarousel({ recipes }) {
  const viewportRef = useRef(null);
  const cardRefs = useRef([]);

  // Physics state lives in refs so animation frames don't re-render React
  const position = useRef(0);
  const velocity = useRef(0);
  const target = useRef(null);
  const frame = useRef(null);
  const lastTime = useRef(0);
  const drag = useRef(null);
  const suppressClick = useRef(false);

  const [activeIndex, setActiveIndex] = useState(0);
  const maxIndex = recipes.length - 1;

  const render = useCallback(() => {
    cardRefs.current.forEach((card, i) => {
      if (!card) return;
      const offset = i - position.current;
      const distance = Math.abs(offset);
      const scale = Math.max(0.6, 1 - distance * 0.14);
      const opacity = Math.max(0, 1 - distance * 0.35);
      const rotate = Math.max(-45, Math.min(45, offset * -18));

      card.style.transform =
        `translateX(calc(-50% + ${offset * CARD_SPACING}px)) ` +
        `translateY(-50%) perspective(900px) rotateY(${rotate}deg) scale(${scale})`;
      card.style.opacity = opacity;
      card.style.zIndex = String(1000 - Math.round(distance * 10));
      card.style.pointerEvents = distance > 2.5 ? "none" : "auto";
    });

    const nearest = Math.round(position.current);
    setActiveIndex((prev) => (prev === nearest ? prev : nearest));
  }, []);

  const step = useCallback(
    function tick(time) {
      const dt = Math.min(64, time - (lastTime.current || time));
      lastTime.current = time;

      if (!drag.current) {
        if (target.current == null) {
          // Coasting: apply momentum with frame-rate independent friction
          position.current += velocity.current * dt;
          velocity.current *= Math.pow(FRICTION, dt / 16);

          // Stop hard at either end
          if (position.current < 0 || position.current > maxIndex) {
            position.current = Math.max(0, Math.min(maxIndex, position.current));
            velocity.current = 0;
          }

          if (Math.abs(velocity.current) < SNAP_SPEED) {
            target.current = Math.round(position.current);
          }
        } else {
          // Snapping: ease toward the target card
          const diff = target.current - position.current;
          position.current += diff * Math.min(1, SNAP_STIFFNESS * (dt / 16));
          if (Math.abs(diff) < 0.001) {
            position.current = target.current;
            target.current = null;
            velocity.current = 0;
            render();
            frame.current = null;
            lastTime.current = 0;
            return;
          }
        }
      }

      render();
      frame.current = requestAnimationFrame(tick);
    },
    [maxIndex, render]
  );

  const startAnimation = useCallback(() => {
    if (frame.current == null) {
      lastTime.current = 0;
      frame.current = requestAnimationFrame(step);
    }
  }, [step]);

  const goTo = useCallback(
    (index) => {
      velocity.current = 0;
      target.current = Math.max(0, Math.min(maxIndex, index));
      startAnimation();
    },
    [maxIndex, startAnimation]
  );

  // Initial layout, and keep position valid if the recipe list changes
  useEffect(() => {
    position.current = Math.max(0, Math.min(maxIndex, position.current));
    render();
  }, [maxIndex, render]);

  useEffect(() => () => cancelAnimationFrame(frame.current), []);

  // Wheel/trackpad: added as a non-passive listener so the page doesn't scroll
  useEffect(() => {
    const viewport = viewportRef.current;
    if (!viewport) return;

    function onWheel(event) {
      const delta =
        Math.abs(event.deltaX) > Math.abs(event.deltaY) ? event.deltaX : event.deltaY;
      const atStart = position.current <= 0 && delta < 0;
      const atEnd = position.current >= maxIndex && delta > 0;
      if (atStart || atEnd) return; // let the page scroll past the ends

      event.preventDefault();
      // deltaMode 1 = lines (e.g. some mice); treat a line as ~40px
      const px = event.deltaMode === 1 ? delta * 40 : delta;
      velocity.current += px * WHEEL_FACTOR;
      target.current = null;
      startAnimation();
    }

    viewport.addEventListener("wheel", onWheel, { passive: false });
    return () => viewport.removeEventListener("wheel", onWheel);
  }, [maxIndex, startAnimation]);

  function onPointerDown(event) {
    if (event.button !== 0) return;
    drag.current = {
      pointerId: event.pointerId,
      startX: event.clientX,
      lastX: event.clientX,
      lastTime: event.timeStamp,
      startPosition: position.current,
      dragging: false,
      samples: [],
    };
    suppressClick.current = false;
    velocity.current = 0;
    target.current = null;
    startAnimation();
  }

  function onPointerMove(event) {
    const d = drag.current;
    if (!d || d.pointerId !== event.pointerId) return;

    const totalDx = event.clientX - d.startX;
    if (!d.dragging && Math.abs(totalDx) > DRAG_THRESHOLD) {
      d.dragging = true;
      suppressClick.current = true;
      // Capture only once dragging so plain clicks still reach the card links
      viewportRef.current.setPointerCapture(event.pointerId);
    }
    if (!d.dragging) return;

    let next = d.startPosition - totalDx / CARD_SPACING;
    // Rubber-band past the ends
    if (next < 0) next *= 0.3;
    if (next > maxIndex) next = maxIndex + (next - maxIndex) * 0.3;
    position.current = next;

    // Keep the last ~100ms of movement to estimate release velocity
    d.samples.push({ x: event.clientX, t: event.timeStamp });
    while (d.samples.length > 2 && event.timeStamp - d.samples[0].t > 100) {
      d.samples.shift();
    }
  }

  function onPointerUp(event) {
    const d = drag.current;
    if (!d || d.pointerId !== event.pointerId) return;
    drag.current = null;

    if (d.dragging && d.samples.length >= 2) {
      const first = d.samples[0];
      const last = d.samples[d.samples.length - 1];
      const dt = Math.max(1, last.t - first.t);
      // A stale sample means the pointer was held still before release
      const fresh = event.timeStamp - last.t < 60;
      velocity.current = fresh ? -(last.x - first.x) / dt / CARD_SPACING : 0;
    }

    if (position.current < 0 || position.current > maxIndex) {
      velocity.current = 0;
      target.current = Math.max(0, Math.min(maxIndex, Math.round(position.current)));
    }
    startAnimation();
  }

  function onCardClick(event, index) {
    if (suppressClick.current) {
      event.preventDefault();
      suppressClick.current = false;
      return;
    }
    // Clicking a side card brings it to the center instead of opening it
    if (index !== activeIndex) {
      event.preventDefault();
      goTo(index);
    }
  }

  function onKeyDown(event) {
    if (event.key === "ArrowRight") {
      event.preventDefault();
      goTo(activeIndex + 1);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      goTo(activeIndex - 1);
    }
  }

  return (
    <section className="recipe-carousel" aria-roledescription="carousel" aria-label="Recipes">
      <div
        ref={viewportRef}
        className="recipe-carousel-viewport"
        tabIndex={0}
        onKeyDown={onKeyDown}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        onDragStart={(e) => e.preventDefault()}
      >
        {recipes.map((recipe, i) => (
          <Link
            key={recipe.id}
            ref={(el) => (cardRefs.current[i] = el)}
            to={`/recipes/${recipe.id}/view`}
            className={`recipe-card${i === activeIndex ? " is-active" : ""}`}
            aria-current={i === activeIndex ? "true" : undefined}
            tabIndex={i === activeIndex ? 0 : -1}
            onClick={(e) => onCardClick(e, i)}
          >
            <h2 className="recipe-card-title">{recipe.title}</h2>
            {recipe.description && (
              <p className="recipe-card-description">{recipe.description}</p>
            )}
            <div className="recipe-card-footer">
              <span className="recipe-card-time">
                <i className="bi bi-clock" aria-hidden="true"></i>{" "}
                {recipe.overall_time != null
                  ? formatTime(recipe.overall_time)
                  : "Not specified"}
              </span>
              <span className="recipe-card-badges">
                {recipe.to_make && <span className="recipe-card-badge to-make">To make</span>}
                {recipe.is_draft && <span className="recipe-card-badge draft">Draft</span>}
              </span>
            </div>
          </Link>
        ))}
      </div>

      <div className="recipe-carousel-controls">
        <button
          type="button"
          onClick={() => goTo(activeIndex - 1)}
          disabled={activeIndex <= 0}
          aria-label="Previous recipe"
        >
          <i className="bi bi-chevron-left" aria-hidden="true"></i>
        </button>
        <span className="recipe-carousel-count" aria-live="polite">
          {activeIndex + 1} / {recipes.length}
        </span>
        <button
          type="button"
          onClick={() => goTo(activeIndex + 1)}
          disabled={activeIndex >= maxIndex}
          aria-label="Next recipe"
        >
          <i className="bi bi-chevron-right" aria-hidden="true"></i>
        </button>
      </div>
    </section>
  );
}
