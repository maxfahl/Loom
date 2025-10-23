// Messy TypeScript file for Prettier to format

   type User = {
  name:string;
    age:  number;
      email:   string;
}

const user: User = {
    name: 'John Doe',
    age:30,
    email: "john.doe@example.com"
}

function    greet( user:User ) {
    console.log( 'Hello, ' + user.name   );
}

greet(user)
