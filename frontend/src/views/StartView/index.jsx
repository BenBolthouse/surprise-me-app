/* eslint-disable react/prop-types */

import React from "react";

import { View, ViewRouteMatchHandler } from "../../components";

export function StartView() {

  return (
    <ViewRouteMatchHandler exact path="/start">
      <View name="start">
        StartView
      </View>
    </ViewRouteMatchHandler>
  )
}
