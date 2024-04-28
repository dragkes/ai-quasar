import { Mutation, MutationTree } from 'vuex';
import { StateInterface } from './state';

interface MutationsInterface extends MutationTree<StateInterface> {
  setOldImage: Mutation<StateInterface> &
    ((state: StateInterface, payload: File) => void);

  setNewImage: Mutation<StateInterface> &
    ((state: StateInterface, payload: File) => void);
}

export default class Mutations implements MutationsInterface {
  setNewImage = (state: StateInterface, payload: File) => {
    state.newImage = payload;
  };

  setOldImage = (state: StateInterface, payload: File) => {
    state.oldImage = payload;
  };

  [key: string]: Mutation<StateInterface>;

};
