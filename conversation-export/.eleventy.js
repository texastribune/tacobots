module.exports = function (eleventyConfig) {
  eleventyConfig.setTemplateFormats([
    'njk',
  ]);
  return {
    dir: {
      input: 'src',
      output: '_site',
    },
  };
};