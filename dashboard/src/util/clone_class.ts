export const clone = (orig: any) => Object.assign(Object.create(Object.getPrototypeOf(orig)), orig)
