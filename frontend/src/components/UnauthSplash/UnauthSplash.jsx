import { useEffect } from "react";
import { Link, useHistory } from "react-router-dom";

import "./UnauthSplash.css";

const UnauthSplash = () => {
  // Hooks
  const history = useHistory();

  // Force the URL to index route
  useEffect(() => {
    history.push("/");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="view unauth-splash">
      <div className="unauth-splash__hook">
        <div className="top">
          <h2>Surprise Me</h2>
          <a>http://benbolt.house</a>
        </div>
        <div>
          <h1>Gift a Friend</h1>
          <p>Send a friend on the hunt for a surprise gift.</p>
          <div className="link-group">
            <Link to="/signup" className="left">Get started</Link>
            <Link to="/login">Sign in</Link>
          </div>
        </div>
      </div>
      <div className="unauth-splash__details">
        <div className="bucket">
          <object data="/images/unauth_bucket_a_badge_320p.svg" type="image/svg+xml" />
          <p>Find a perfect gift for a friend from local businesses</p>
        </div>
        <div className="bucket">
          <object data="/images/unauth_bucket_b_badge_320p.svg" type="image/svg+xml" />
          <p>Send a friend on the hunt to find the gift</p>
        </div>
        <div className="bucket">
          <object data="/images/unauth_bucket_c_badge_320p.svg" type="image/svg+xml" />
          <p>They won't discover what the surprise is until they find it!</p>
        </div>
      </div>
      <div className="unauth-splash__cta">
        <div>
          <h2>Pretty simple, huh?</h2>
          <p><Link to="/signup">Sign up</Link> to send a gift to a friend!</p>
        </div>
      </div>
    </div>
  )
}
export default UnauthSplash;
