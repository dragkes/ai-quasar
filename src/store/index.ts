import Mutations from './mutations';
import type { InjectionKey } from 'vue';
import { State, StateInterface } from './state';
import { createStore, useStore as baseUseStore, Store } from 'vuex';

export type StoreType = Store<StateInterface>;

export const key: InjectionKey<StoreType> = Symbol();

const store = createStore<StateInterface>({
  mutations: new Mutations(),
  state: new State(),
});

export function useStore(): StoreType {
  return baseUseStore(key);
}

export default store;
