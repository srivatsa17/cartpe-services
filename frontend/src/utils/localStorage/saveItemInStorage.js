import secureLocalStorage from 'react-secure-storage';

const saveItemInStorage = (storageItemKey, storageItemValue) => {
    secureLocalStorage.setItem(storageItemKey, JSON.stringify(storageItemValue));
}

export default saveItemInStorage