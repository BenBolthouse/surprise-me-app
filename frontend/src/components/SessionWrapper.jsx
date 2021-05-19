// eslint-disable-next-line no-unused-vars
import { ReactElement, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";

import * as actions from "../store/actions";

/**
 * Component sits below the high order components in the tree to handle
 * fetching user and user-related data on render. Component also handles
 * redirection to a sign in page when a session isn't available.
 * @param {object} props
 * @return {ReactElement}
 */
export const Authenticated = ({ children }) => {
  const dispatch = useDispatch();
  const session = useSelector(x => x.session);
  const history = useHistory();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (!session.active) history.push("/sign-in");
    else {
      dispatch(actions.user.get());
      dispatch(actions.connections.get());

      setMounted(true);
    }
  }, [session.active]);

  return !mounted ? null : children;
};

/**
 * Component sits below the high order components in the tree and handles
 * redirection to the app when a session exists, so as to avoid
 * unauthenticated actions from occurring while the user is authenticated.
 * @param {object} props
 * @return {ReactElement}
 */
export const Anonymous = ({ children }) => {
  const session = useSelector(x => x.session);
  const history = useHistory();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (session.active) history.push("/");

    else setMounted(true);
  }, [session.active]);

  return !mounted ? null : children;
}