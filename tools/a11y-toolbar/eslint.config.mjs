import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist/**', '*.mjs'] },
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: { parserOptions: { project: './tsconfig.json', tsconfigRootDir: import.meta.dirname } },
    rules: {
      '@typescript-eslint/restrict-template-expressions': ['error', { allowNumber: true }],
      '@typescript-eslint/no-confusing-void-expression': ['error', { ignoreArrowShorthand: true }],
    },
  },
);
