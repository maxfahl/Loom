// dip_good_bad.ts

// BAD Example (violates DIP)
class MySQLDatabaseDIPBad {
  save(data: string): void {
    console.log(`Saving "${data}" to MySQL database.`);
  }
}

class UserServiceDIPBad {
  private db: MySQLDatabaseDIPBad;

  constructor() {
    this.db = new MySQLDatabaseDIPBad(); // Direct dependency on a concrete low-level module
  }

  saveUserData(data: string): void {
    this.db.save(data);
  }
}

// GOOD Example (adheres to DIP)

interface DatabaseDIP {
  save(data: string): void;
}

class MySQLDatabaseDIP implements DatabaseDIP {
  save(data: string): void {
    console.log(`Saving "${data}" to MySQL database.`);
  }
}

class MongoDBDatabaseDIP implements DatabaseDIP {
  save(data: string): void {
    console.log(`Saving "${data}" to MongoDB database.`);
  }
}

class UserServiceDIP {
  private db: DatabaseDIP; // Depends on the abstraction, not a concrete implementation

  constructor(db: DatabaseDIP) { // Dependency Injection
    this.db = db;
  }

  saveUserData(data: string): void {
    this.db.save(data);
  }
}

// Usage
const mySqlDbDIP = new MySQLDatabaseDIP();
const userServiceWithMySQLDIP = new UserServiceDIP(mySqlDbDIP);
userServiceWithMySQLDIP.saveUserData("User data for MySQL");

const mongoDbDIP = new MongoDBDatabaseDIP();
const userServiceWithMongoDBDIP = new UserServiceDIP(mongoDbDIP);
userServiceWithMongoDBDIP.saveUserData("User data for MongoDB");
