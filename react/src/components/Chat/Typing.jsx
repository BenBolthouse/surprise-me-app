import { useEffect, useState } from "react";

const Typing = ({ usersName }) => {

  const [ellipsis, setEllipsis] = useState(".");
  const BLINK_SPEED = 500;

  useEffect(() => {
    const blink = setInterval(() => {
      if (ellipsis.length >= 3) setEllipsis(".");
      else setEllipsis(ellipsis + ".");
    }, BLINK_SPEED);
    return () => {
      clearInterval(blink)
    };
  });

  return (<p>{usersName} is typing{ellipsis}</p>);
};

export default Typing;
