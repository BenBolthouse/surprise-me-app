/* eslint-disable react/prop-types */

import { useRouteMatch } from "react-router-dom";

import {
  cloneElement as clone,
  createElement as element,
  Fragment,
} from "react";

import "./styles.css";

function viewRouteMatchHandler(props) {
  let { path, exact, children } = props;

  const active = useRouteMatch({
    path,
    exact,
  });

  children = clone(children, { ...children.props, matching: active });

  return element(Fragment, null, children);
}

export function ViewRouteMatchHandler(props) {
  return element(viewRouteMatchHandler, props);
}

export function View(props) {
  const { name, matching, children } = props;

  // prettier-ignore
  function getMatchingAttributeOrObject() {
    if (matching !== undefined && matching) {
      return { "br-view-match": "match" };
    }
    else if (matching !== undefined && !matching) {
      return { "br-view-match": "no-match" };
    }
    else {
      return {};
    }
  }

  const viewElement = {
    className: "view " + name + "-view",
    ...getMatchingAttributeOrObject(),
  };

  return element("div", viewElement, children);
}
