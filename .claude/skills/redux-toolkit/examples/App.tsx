import React from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import CounterComponent from './features/counter/CounterComponent';
import PostsList from './features/posts/PostsList';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <div style={{ padding: '20px' }}>
        <h1>Redux Toolkit Example App</h1>
        <CounterComponent />
        <hr />
        <PostsList />
      </div>
    </Provider>
  );
};

export default App;
