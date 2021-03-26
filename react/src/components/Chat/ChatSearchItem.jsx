import { Link } from "react-router-dom";

import ImagePreload from "../ImagePreload/ImagePreload";

const ChatSearchItem = ({resultObject: res}) => {
  const ous = res.otherUser;
  return (
    <Link to={"/messages/" + res.id}>
      <li className="search-result-item">
        <ImagePreload src={`/f/profile_${ous.id}_64p.jpg`} />
        <p>{ous.firstName} {ous.lastName}</p>
      </li>
    </Link>
  );
}

export default ChatSearchItem;
