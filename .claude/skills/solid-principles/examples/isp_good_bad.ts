// isp_good_bad.ts

// BAD Example (violates ISP)
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  manageTeam(): void; // Not all workers manage teams
  code(): void;       // Not all workers code
}

class DeveloperISPBad implements Worker {
  work(): void { console.log("Developer is coding."); }
  eat(): void { console.log("Developer is eating."); }
  sleep(): void { console.log("Developer is sleeping."); }
  manageTeam(): void { /* Does nothing, forced to implement */ }
  code(): void { console.log("Developer is writing code."); }
}

class JanitorISPBad implements Worker {
  work(): void { console.log("Janitor is cleaning."); }
  eat(): void { console.log("Janitor is eating."); }
  sleep(): void { console.log("Janitor is sleeping."); }
  manageTeam(): void { /* Does nothing, forced to implement */ }
  code(): void { /* Does nothing, forced to implement */ }
}

// GOOD Example (adheres to ISP)

interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

interface Codeable {
  code(): void;
}

interface Manageable {
  manageTeam(): void;
}

class DeveloperISP implements Workable, Eatable, Sleepable, Codeable {
  work(): void { console.log("Developer is working."); }
  eat(): void { console.log("Developer is eating."); }
  sleep(): void { console.log("Developer is sleeping."); }
  code(): void { console.log("Developer is writing code."); }
}

class JanitorISP implements Workable, Eatable, Sleepable {
  work(): void { console.log("Janitor is cleaning."); }
  eat(): void { console.log("Janitor is eating."); }
  sleep(): void { console.log("Janitor is sleeping."); }
}

class ManagerISP implements Workable, Eatable, Sleepable, Manageable {
  work(): void { console.log("Manager is attending meetings."); }
  eat(): void { console.log("Manager is eating."); }
  sleep(): void { console.log("Manager is sleeping."); }
  manageTeam(): void { console.log("Manager is managing the team."); }
}
