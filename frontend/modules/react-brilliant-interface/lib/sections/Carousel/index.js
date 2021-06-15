/* eslint-disable react/prop-types */

import {
  cloneElement,
  createElement,
  Fragment,
  useState,
} from "react";

export function Carousel(props) {
  let { name, children } = props;

  const _framesCount = children.length;

  /** Contains an index of the currently visible frame */
  const [_framePosition, _setFramePosition] = useState(0);

  /**
   * Sets the framePosition state to the index of a particular frame.
   */
  function _goFrame(index) {
    _setFramePosition(index);
  }

  /**
   * Increments framePosition or starts over at the first frame.
   */
  function _goNextFrame() {
    if (_framesCount <= _framePosition + 1) _setFramePosition(0);
    else _setFramePosition(_framePosition + 1);
  }

  /**
   * Decrements framePosition or moves to the last frame.
   */
  function _goPrevFrame() {
    if (_framePosition === 0) _setFramePosition(_framesCount - 1);
    else _setFramePosition(_framePosition - 1);
  }

  /**
   * Adds props **active** and **_goNextFrame** to each child.
   */
  function cloneChildrenWithProps() {
    const childrenArray = Array.isArray(children) ? children : [children];

    return childrenArray.map((child, i) => {
      return cloneElement(child, {
        _goNextFrame,
        _active: _framePosition === i,
        speed: child.props.speed,
        key: name + "-br-carousel-frame-" + i,
        index: i,
      });
    });
  }

  const carouselElement = {
    className: "br-carousel " + name,
  };

  const frameContainerElement = {
    className: "br-carousel-frame-container",
    style: {
      left: _framePosition * -100 + "vw",
      width: _framesCount * 100 + "vw",
    },
  };

  const prevFrameElement = {
    className: "br-carousel-controls prev-frame",
    onClick: () => _goPrevFrame(),
    tabIndex: "-1",
  };

  const nextFrameElement = {
    className: "br-carousel-controls next-frame",
    onClick: () => _goNextFrame(),
    tabIndex: "-1",
  };

  const thumbnailTrayComponent = {
    _framesCount,
    _goFrame,
    _framePosition,
    _name: name,
  };

  return createElement(
    "div",
    carouselElement,
    createElement(
      "div",
      frameContainerElement,
      cloneChildrenWithProps()
    ),
    _framesCount <= 1
      ? null
      : createElement(
          Fragment,
          null,
          createElement("button", prevFrameElement),
          createElement("button", nextFrameElement),
          createElement(ThumbnailTray, thumbnailTrayComponent, children)
        )
  );
}

function ThumbnailTray(props) {
  let { _framesCount, _goFrame, _framePosition, _name } = props;

  let thumbnailsElements = [];

  for (let i = 0; i < _framesCount; i++) {
    thumbnailsElements.push(
      createElement("div", {
        className: "br-carousel-thumbnail " + (_framePosition === i ? "active" : "not-active"),
        key: _name + "-carousel-thumbnail-" + i,
        onClick: () => _goFrame(i),
      })
    );
  }

  const thumbnailTrayElement = {
    className: "br-carousel-thumbnail-tray",
  };

  return createElement("div", thumbnailTrayElement, thumbnailsElements);
}
