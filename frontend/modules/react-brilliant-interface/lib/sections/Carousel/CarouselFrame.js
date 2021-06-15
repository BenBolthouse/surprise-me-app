/* eslint-disable react/prop-types */

import {
  createElement,
  useEffect,
} from "react";

import "./styles.css";

export function CarouselFrame(props) {
  let { name, speed, children, _goNextFrame, _active } = props;

  /**
   * Side effect handles the timeout of the active frame and cleanup of the
   * timeout function.
   */
  useEffect(() => {
    let timeout;
    if (_active) timeout = setTimeout(() => _goNextFrame(), speed * 1000);
    return () => clearTimeout(timeout);
  }, [_active]);

  const frameElement = {
    className: "br-carousel-frame " + name,
  };

  const progressContainerElement = {
    className: "br-carousel-frame-progress-container",
  };

  const progressElement = {
    className: "br-carousel-frame-progress",
    style: {
      animation: _active ? `br-carousel-frame-progress ${speed}s linear 0s 1 forwards` : "none",
    },
  };

  return createElement("div", frameElement,
    children,
    createElement(
      "div",
      progressContainerElement,
      createElement("div", progressElement)
    )
  );
}
