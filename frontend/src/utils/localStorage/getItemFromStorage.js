import secureLocalStorage from 'react-secure-storage';

const getItemFromStorage = (storageItemKey) => {
    const storageItemDetails = secureLocalStorage.getItem(storageItemKey)
    return storageItemDetails ? JSON.parse(storageItemDetails) : null
}

export default getItemFromStorage