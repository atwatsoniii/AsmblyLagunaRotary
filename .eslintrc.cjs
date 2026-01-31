module.exports = {
  root: true,
  env: { es6: true },
  overrides: [
    {
      files: ["*.cps"],
      parserOptions: { ecmaVersion: 2020 },
    },
  ],
};
