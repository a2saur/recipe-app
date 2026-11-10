import { useEffect } from "react";

// Shows the gingham page background while the calling page is mounted
export function useBackground(bgClass) {
  useEffect(() => {
    document.documentElement.classList.add(bgClass);
    return () => document.documentElement.classList.remove(bgClass);
  }, []);
}