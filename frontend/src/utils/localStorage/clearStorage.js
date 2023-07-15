import secureLocalStorage from "react-secure-storage"

const clearStorage = () => {
    secureLocalStorage.clear()
}

export default clearStorage