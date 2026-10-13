/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

  jsxSingleQuote: false,
  trailingComma: "es5",
  bracketSpacing: true,
  arrowParens: "always",
  endOfLine: "lf",
  importOrder: [
    "",
    "<THIRD_PARTY_MODULES>", // Imports not matched by other special words or groups.
    "",
    "<BUILTIN_MODULES>", // Node.js built-in modules
    "",
    "^(@js|@translations)/(.*)$",
    "^/(.*)$",
    "",
    "^[.]", // relative imports
  ],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
};

export default config;
