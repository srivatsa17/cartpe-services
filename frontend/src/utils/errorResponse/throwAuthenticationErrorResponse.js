const throwAuthenticationErrorResponse = (error) => {
    return error.response && error.response.data.detail ? error.response.data.detail : error.message
}

export default throwAuthenticationErrorResponse