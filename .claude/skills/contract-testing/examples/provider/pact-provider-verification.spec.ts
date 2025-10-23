// examples/provider/pact-provider-verification.spec.ts

import { Verifier } from '@pact-foundation/pact';
import * as path from 'path';

// This example assumes your User API is running on http://localhost:3000
// You would typically start your provider service before running this verification.

const providerBaseUrl = process.env.PROVIDER_BASE_URL || 'http://localhost:3000';
const pactBrokerUrl = process.env.PACT_BROKER_URL;
const pactBrokerToken = process.env.PACT_BROKER_TOKEN;
const publishVerificationResults = process.env.PUBLISH_VERIFICATION_RESULTS === 'true';
const providerVersion = process.env.PROVIDER_VERSION || '1.0.0';

// Define the provider states. These functions will be called by the Pact Verifier
// to set up the provider service in the correct state before each interaction is replayed.
const providerStates = {
  'user exists': () => {
    console.log('Provider State: user exists - ensuring user with ID 1 is available.');
    // In a real application, you would interact with your database or service
    // to ensure the state is met. For this example, our user-api.ts handles it
    // via a custom header 'x-pact-provider-state'.
  },
  'a request to create a new user': () => {
    console.log('Provider State: a request to create a new user - no specific setup needed for this example.');
  },
  // Add other provider states as needed
};

describe('Pact Provider Verification', () => {
  it('should validate the expectations of all consumers', async () => {
    const opts: any = {
      provider: 'UserService',
      providerBaseUrl: providerBaseUrl,
      // Fetch pacts from the Pact Broker
      pactBrokerUrl: pactBrokerUrl,
      pactBrokerToken: pactBrokerToken,
      publishVerificationResult: publishVerificationResults,
      providerVersion: providerVersion,
      // Filter pacts to verify (e.g., by consumer, tag)
      // consumerVersionSelectors: [{ tag: 'master', latest: true }],
      // consumerVersionSelectors: [{ branch: 'main', latest: true }],
      // Or specify local pact files for development/testing without a broker
      // pactUrls: [path.resolve(process.cwd(), './pact/interactions/frontendapp-userservice.json')],
      logLevel: 'debug',
      stateHandlers: providerStates,
      requestFilter: (req, res, next) => {
        // Add a custom header to simulate provider states being passed to the API
        // This is a simple example; a real implementation might use a dedicated endpoint
        // or modify the request body/query params based on the state.
        if (req.headers && req.headers['x-pact-provider-state']) {
          req.headers['x-pact-provider-state'] = req.headers['x-pact-provider-state'];
        }
        next();
      },
    };

    if (!pactBrokerUrl) {
      console.warn('PACT_BROKER_URL not set. Verification will run against local pact files if specified, otherwise it will fail.');
      // Fallback to local pact files if no broker URL is provided
      opts.pactUrls = [path.resolve(process.cwd(), './pact/interactions/frontendapp-userservice.json')];
    }

    try {
      await new Verifier(opts).verifyProvider();
      console.log('Pact Verification Complete!');
    } catch (error) {
      console.error('Pact Verification Failed:', error);
      throw error;
    }
  });
});
