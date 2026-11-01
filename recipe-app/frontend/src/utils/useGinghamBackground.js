import { useEffect } from "react";

// Shows the gingham page background while the calling page is mounted
export function useGinghamBackground() {
  useEffect(() => {
    document.documentElement.classList.add("gingham-bg");
    return () => document.documentElement.classList.remove("gingham-bg");
  }, []);
}
