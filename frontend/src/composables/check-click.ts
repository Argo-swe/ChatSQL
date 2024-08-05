/**
 * Checks if the target element is either the same as the given element or is a descendant of it.
 * @param element - The element to check against the target.
 * @param target - The target of the event to check.
 */
const checkNodeRelation = (element: Element | null, target: EventTarget | null): boolean =>
  element !== null &&
  target instanceof Node &&
  (element.isSameNode(target) || element.contains(target));

/**
 * Determines if a click event occurred outside of the specified elements.
 * @param event - The click event to check.
 * @param selectors - An array of CSS selectors to match against.
 */
const isOutsideClicked = (event: Event, selectors: string[]): boolean => {
  const target = event.target;

  return selectors.every((selector) => {
    const element = document.querySelector(selector);
    return !checkNodeRelation(element, target);
  });
};

/**
 * Composable function for checking if a click event occurred outside of specified elements.
 * @param selectors - An array of CSS selectors to match against.
 */
export function useCheckOutsideClick(selectors: string[]) {
  return {
    isOutsideClicked: (event: Event) => isOutsideClicked(event, selectors)
  };
}
