import '@testing-library/jest-dom';
import axios from 'axios';

axios.defaults.adapter = 'fetch';

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
});

Element.prototype.scrollIntoView = () => {};

Object.defineProperty(document, 'scrollingElement', {
  value: document.documentElement,
  writable: true,
});

window.resizeTo = () => {};
