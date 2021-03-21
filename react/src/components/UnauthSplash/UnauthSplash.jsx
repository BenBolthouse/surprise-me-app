import { useEffect } from "react";
import { useHistory } from "react-router-dom";

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
        <h1>Gift a Friend</h1>
        <p>Send a friend on the hunt for a surprise gift.</p>
      </div>
      <div className="unauth-splash__details">
        <div className="unauth-splash__details-bucket-a">
          <img src="/f/unauth_bucket_a_badge_320.svg" alt="" />
          <p>Find a perfect gift for a friend from local businesses</p>
        </div>
        <div className="unauth-splash__details-bucket-b">
          <img src="/f/unauth_bucket_b_badge_320.svg" alt="" />
          <p>Send a friend on the hunt to find the gift</p>
        </div>
        <div className="unauth-splash__details-bucket-c">
          <img src="/f/unauth_bucket_c_badge_320.svg" alt="" />
          <p>They won't discover what the surprise is until they find it!</p>
        </div>
      </div>
      <div className="unauth-splash__cta">
        <h2>Are you in?</h2>
        <p>Sign up to send a gift to a friend!</p>
      </div>
    </div>
  )
}
export default UnauthSplash;
