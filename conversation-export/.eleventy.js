module.exports = function (eleventyConfig) {
  eleventyConfig.setTemplateFormats([
    'md',
    'njk',
  ]);
  return {
    dir: {
      input: 'src',
      output: '_site',
    },
  };
};