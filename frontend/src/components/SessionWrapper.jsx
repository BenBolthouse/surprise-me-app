import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useHistory } from "react-router-dom";

export const Authenticated = ({ children }) => {
  const session = useSelector(x => x.session);
  const history = useHistory();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Immediately redirect if the session doesn't exist...
    if (!session.active) history.push("/sign-in");
    // Otherwise begin fetching data.
    else {
      console.log("Starting session context wrapper actions...");
      // ...

      setMounted(true);
    }
  }, [session.active]);

  return !mounted ? null : children;
};

export const Anonymous = ({ children }) => {
  const session = useSelector(x => x.session);
  const history = useHistory();

  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Immediately redirect to the app if the session exists...
    if (session.active) history.push("/");
    // Otherwise set the components as mounted.
    else setMounted(true);
  }, [session.active]);

  return !mounted ? null : children;
}
