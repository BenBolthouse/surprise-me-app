import { denormalize } from "../../services/normalize";

export const searchConnections = (connections, term) => {
  const utm = term.toUpperCase();
  const est = denormalize(connections.established);
  const out = est.filter((con) => {
    const ous = con.otherUser;
    const fst = ous.firstName.toUpperCase().includes(utm);
    const lst = ous.lastName.toUpperCase().includes(utm);
    if (fst || lst) return true;
    else return false;
  });
  if (out.length > 10) {
    const slc = out.slice(0, 9);
    return slc;
  }
  else return out;
};
