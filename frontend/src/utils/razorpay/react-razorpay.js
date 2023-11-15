import { useCallback, useEffect, useMemo, useState } from "react";

class Razorpay {
    constructor(options) {
        this.options = options;
        if (typeof window !== "undefined")
            this.razorpayInstance = new window.Razorpay(this.options);
    }

    on(event, callback) {
        this.razorpayInstance.on(event, callback);
    }

    open() {
        this.razorpayInstance.open();
    }
}

const useRazorpay = () => {
    /* Constants */
    const RAZORPAY_SCRIPT = "https://checkout.razorpay.com/v1/checkout.js";

    const isClient = useMemo(() => typeof window !== "undefined", []);

    const [isLoaded, setIsLoaded] = useState(false);

    const checkScriptLoaded = useCallback(() => {
        if (!isClient || !("Razorpay" in window))
            return false;
        return true;
    }, [isClient]);

    const loadScript = useCallback((scriptUrl) => {
        if (!isClient)
            return; // Don't execute this function if it's rendering on the server side
        return new Promise((resolve, reject) => {
            const scriptTag = document.createElement("script");
            scriptTag.src = scriptUrl;
            scriptTag.onload = (ev) => {
                setIsLoaded(true);
                resolve(ev);
            };
            scriptTag.onerror = (err) => reject(err);
            document.body.appendChild(scriptTag);
        });
    }, [isClient]);

    useEffect(() => {
        if (!checkScriptLoaded()) {
            (async () => {
                try {
                    await loadScript(RAZORPAY_SCRIPT);
                } catch (error) {
                    throw new Error(error);
                }
            })();
        }
    }, [checkScriptLoaded, loadScript]);

    return [Razorpay, isLoaded];
};

export default useRazorpay;
