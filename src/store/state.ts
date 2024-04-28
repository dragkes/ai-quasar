export interface StateInterface {
  newImage: File | null,
  oldImage: File | null,
}

export class State implements StateInterface {
  newImage: File | null = null;
  oldImage: File | null = null;
}

export default State;
