module.exports = {
    verbose: true,
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
    testEnvironment: 'jest-environment-jsdom',
    testPathIgnorePatterns: ['<rootDir>/node_modules/', "<rootDir>/build/"],
    moduleNameMapper: {
      '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$': '<rootDir>/__mocks__/fileMock.js',
      '\\.(css|less)$': 'identity-obj-proxy',
    },
    collectCoverage: true,
    coverageReporters: ["json", "html", "text"],
    collectCoverageFrom: ['<rootDir>/src/components/*.js'],
};