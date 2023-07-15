import getItemFromStorage from './getItemFromStorage';
import saveItemInStorage from './saveItemInStorage';

const updateItemInStorage = (storageItemKey, storageItemFields) => {
    const storageItem = getItemFromStorage(storageItemKey)
    if(storageItem) {
        Object.keys(storageItemFields).forEach((fieldName) => {
            storageItem[fieldName] = storageItemFields[fieldName]
        })
        saveItemInStorage(storageItemKey, storageItem)
    }
}

export default updateItemInStorage