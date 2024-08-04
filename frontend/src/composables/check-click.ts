const checkNodeRelation = (element: Element | null, target: EventTarget | null): boolean =>
  element !== null &&
  target instanceof Node &&
  (element.isSameNode(target) || element.contains(target));

const isOutsideClicked = (event: Event, selectors: string[]) => {
  const target = event.target;

  return selectors.every((selector) => {
    const element = document.querySelector(selector);
    return !checkNodeRelation(element, target);
  });
};

export function useCheckOutsideClick(selectors: string[]) {
  return {
    isOutsideClicked: (event: Event) => isOutsideClicked(event, selectors)
  };
}
