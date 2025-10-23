// srp_good_bad.ts

// BAD Example (violates SRP)
class UserSettings {
  constructor(private user: { id: string; name: string; email: string }) {}

  changeUsername(newUsername: string): void {
    // Logic to validate and update username in database
    console.log(`Username changed to ${newUsername}`);
  }

  changeEmail(newEmail: string): void {
    // Logic to validate and update email in database
    console.log(`Email changed to ${newEmail}`);
  }

  sendNotification(message: string): void {
    // Logic to send email/push notification to user
    console.log(`Notification sent to ${this.user.email}: ${message}`);
  }

  logActivity(activity: string): void {
    // Logic to log user activity to a file or monitoring service
    console.log(`Activity logged for ${this.user.name}: ${activity}`);
  }
}

// GOOD Example (adheres to SRP)

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserRepository {
  updateUser(user: User): void;
}

interface NotificationService {
  send(to: string, message: string): void;
}

interface Logger {
  log(message: string): void;
}

class UserProfileManager {
  constructor(private user: User, private userRepository: UserRepository) {}

  changeUsername(newUsername: string): void {
    // Validate username
    this.user.name = newUsername;
    this.userRepository.updateUser(this.user);
    console.log(`Username changed to ${newUsername}`);
  }

  changeEmail(newEmail: string): void {
    // Validate email
    this.user.email = newEmail;
    this.userRepository.updateUser(this.user);
    console.log(`Email changed to ${newEmail}`);
  }
}

class UserNotifier {
  constructor(private user: User, private notificationService: NotificationService) {}

  sendNotification(message: string): void {
    this.notificationService.send(this.user.email, message);
    console.log(`Notification sent to ${this.user.email}: ${message}`);
  }
}

class UserActivityLogger {
  constructor(private user: User, private logger: Logger) {}

  logActivity(activity: string): void {
    this.logger.log(`Activity logged for ${this.user.name}: ${activity}`);
  }
}
