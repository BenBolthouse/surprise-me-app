import { EntityBase } from "../entity";

class Session extends EntityBase {
  constructor() {
    super(
      {
        csrfToken: "String",
      },
      {}
    );
  }
}

const sessionManager = new Session();

export default sessionManager;
