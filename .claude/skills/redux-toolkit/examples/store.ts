import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './features/counter/counterSlice';
import postsReducer from './features/posts/postsSlice';
import { postsApi } from './features/posts/postsApi';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    posts: postsReducer,
    [postsApi.reducerPath]: postsApi.reducer,
  },
  // Adding the api middleware enables caching, invalidation, polling, and other useful features of RTK Query.
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(postsApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
