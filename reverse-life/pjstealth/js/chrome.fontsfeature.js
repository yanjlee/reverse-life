var rand = {
    "noise": function () {
        var SIGN = Math.random() < Math.random() ? -1 : 1;
        return Math.floor(Math.random() + SIGN * Math.random());
    },
    "sign": function () {
        const tmp = [-1, -1, -1, -1, -1, -1, +1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1];
        const index = Math.floor(Math.random() * tmp.length);
        return tmp[index];
    }
};
Object.defineProperty(HTMLElement.prototype, "offsetHeight", {
    get() {
        let height = 500;
        try {
            height = Math.floor(this.getBoundingClientRect().height);
        } catch (e) {
            height = Math.floor(this.clientHeight)
        }
        const valid = height && rand.sign() === 1;
        const result = valid ? height + rand.noise() : height;
        return result;
    }
});

Object.defineProperty(HTMLElement.prototype, "offsetWidth", {
    get() {
        let width = 500;
        try {
            width = Math.floor(this.getBoundingClientRect().width);
        } catch (e) {
            width =  Math.floor(this.clientWidth)
        }
        const valid = width && rand.sign() === 1;
        const result = valid ? width + rand.noise() : width;
        return result;
    }
});
