/* eslint-disable react/prop-types */

import React from "react";
import { Link, useRouteMatch } from "react-router-dom";

import "./styles.css";

export function StartView() {
  const pathMatch = useRouteMatch({
    path: "/start",
    exact: true,
  });

  const viewComponent = {
    className: "view start-view",
    "view-path-match": pathMatch ? "match" : "no-match",
  }

  return (
    <div {...viewComponent}>
      <Link to="/start/sign-in">Sign In</Link>
    </div>
  )
}
