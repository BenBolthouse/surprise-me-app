import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import * as connectionsActions from "../../store/reducers/connections";
import * as notificationsActions from "../../store/reducers/notifications";

/**
 * Wraps a high-order component to provide a five-second
 * beat to access state changes on the backend API.
 * @param {*} props React props
 */
const HeartbeatApiAccess = ({ children }) => {
  // Hooks
  const dispatch = useDispatch()
  const connections = useSelector(s => s.connections)

  // Component state
  const [mounted, setMounted] = useState(false);

  const sendPulse = async () => {
    window.syncMessageCounts = setTimeout(async () => {
      // Actions to commit during pulse...
      await dispatch(
        await connectionsActions.updateEstConnections()
      )

      // Keep looping indefinitely. This design was chosen
      // over a setInterval implementation so that any
      // hanging requests pause the beat.
      sendPulse()
    }, 5000)
  }

  useEffect(() => {

    if (mounted) {
      // Once mounted run a request to get all of the user's
      // established connections for Redux state.
      sendPulse()
    }
    else {
      // On pre-mount get all of the user's established
      // connections for Redux state...
      dispatch(connectionsActions.getEstConnectionsOnLoad())

        // Then get notifications from the client local
        // storage or create one by default...
        .then(() =>
          dispatch(notificationsActions.syncReduxLocalOnLoad()))

        // Then set the component to mounted. 
        .finally(() => setMounted(true))
    }

    // Cleanup async functions on un-mount.
    return () => window.clearTimeout(window.syncMessageCounts)

  }, [mounted])

  return children;
}

export default HeartbeatApiAccess;
