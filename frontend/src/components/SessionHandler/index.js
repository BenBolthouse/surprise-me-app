/* eslint-disable react/prop-types */

import { actions } from "../../store";
import { createElement, Fragment, useEffect, useState } from "react";
import { Redirect } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";

export function SessionHandler(props) {
  const { children } = props;

  const dispatch = useDispatch();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    async function go() {
      const active = await dispatch(actions.session.get());

      // Here we invoke hooks to retrieve data to build the user
      // experience. In the last step we'll assign "true" to a state
      // variable allowing this component's elements to render.
      //
      // Place your data request hooks here. Remember to await them because
      // you'll likely have dependent hooks.
      if (active === true) {
        await dispatch(actions.user.get())

      }
      // Final step of the data retrieval side effect is setting the
      // mount. It's important that this line is invoked finally after
      // hooks to ensure clean app rendering!
      setMounted(true);
    }
    go();
  }, []);

  return mounted ? createElement(Fragment, null, children) : null;
}

export function Authenticated(props) {
  let { redirect, children } = props;

  const session = useSelector((s) => s.session);

  if (!redirect || typeof redirect !== "string") redirect = "/";

  if (!session.active) {
    return createElement(Redirect, { to: redirect });
  }
  else return createElement(Fragment, null, children);
}

export function Anonymous(props) {
  let { redirect, children } = props;

  const session = useSelector((s) => s.session);

  if (!redirect || typeof redirect !== "string") redirect = "/";

  if (session.active) {
    return createElement(Redirect, { to: redirect });
  }
  else return createElement(Fragment, null, children);
}
