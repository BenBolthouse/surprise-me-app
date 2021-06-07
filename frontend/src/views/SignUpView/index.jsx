/* eslint-disable no-unused-vars */

import React, { createContext, useState } from "react";

import { View } from "../../components";

export const SignUpContext = createContext();

export function SignUpView() {
  const [viewState, setViewState] = useState({
    firstName: {
      value: "",
      errors: [],
    },
    lastName: {
      value: "",
      errors: [],
    },
    email: {
      value: "",
      errors: [],
    },
    password: {
      value: "",
      errors: [],
    },
    confirmPassword: {
      value: "",
      errors: [],
    },
    profileImage: {
      value: null,
      errors: [],
    },
    bio: {
      value: "",
      errors: [],
    },
    approveLocationService: {
      value: false,
      errors: [],
    },
  });

  return (
    <SignUpContext.Provider value={{ viewState, setViewState }}>
      <View name="sign-up">
        <div>Hello</div>
      </View>
    </SignUpContext.Provider>
  )
}
