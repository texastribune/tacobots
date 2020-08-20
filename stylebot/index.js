// Load the base using the Airtable package
const base = require("airtable").base(process.env.AIRTABLE_BASE_ID);
// lamdbda handler function
exports.handler = async function (event, context) {
  // validate slack token
  if (event.token !== process.env.SLACK_TOKEN) {
    return {
      response_type: "ephemeral",
      text: "Something is wrong with your Slack token."
    }
  }
  const commandText = event.text;
  const dictResults = await queryStyleGuide(commandText);
  if (dictResults != "") {
    return {
      response_type: "in_channel",
      text: dictResults,
    };
  } else {
    return {
      response_type: "in_channel",
      text: `Unfortunately, I couldn't find an entry for \`${commandText}\`. Please try a different entry or check the <${process.env.STYLEGUIDE_URL}|Style Guide>.`,
    };
  }
};
// Create async function that can be called when executed.
async function queryStyleGuide(searchValue) {
  try {
    const results = await new Promise((resolve, reject) => {
      base("dictionary")
        .select({
          // Check if the value entered matches any of the entries in the table
          filterByFormula: `SEARCH('${searchValue}', LOWER({Name}))`,
        })
        .firstPage(function (err, records) {
          if (err) {
            return reject(err);
          }
          const definitions = [];
          // For each match, add the name and notes to
          records.forEach(function (record) {
            const name = record.get("Name");
            const notes = record.get("Notes");
            const entry = `*${name}:*\n${notes}`;
            definitions.push(entry);
          });
          resolve(definitions);
        });
    });
    // Return the full list of definitions; separated by two new lines
    return results.join("\n\n");
  } catch (err) {
    // do something with error
  }
}