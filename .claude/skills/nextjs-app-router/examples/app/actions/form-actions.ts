"use server";

import { revalidatePath } from 'next/cache';

export async function submitFormAction(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  console.log(`Server Action: submitFormAction received - Name: ${name}, Email: ${email}`);

  // Simulate a database operation
  await new Promise(resolve => setTimeout(resolve, 1000));

  // In a real application, you would save this data to a database
  // and handle any errors.

  // Revalidate the path to update any cached data that depends on this form submission
  revalidatePath('/server-action-form'); // Revalidate the page where the form is displayed

  return { message: `Form submitted successfully for ${name}!` };
}
