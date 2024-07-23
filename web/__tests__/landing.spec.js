/**
 * @jest-environment jsdom
 */

const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.resolve(__dirname, '../index.html'), 'utf8');

jest
  .dontMock('fs');

describe('button', function () {
  beforeEach(() => {
    document.documentElement.innerHTML = html.toString();
  });

  afterEach(() => {
    // restore the original func after test
    jest.resetModules();
  });

  it('Has the right title', function () {
    expect(document.title.trim()).toEqual('Forecast FC');
  });

  it('Links to team schedule', function () {
    expect(document.body.innerHTML.includes("full season schedule"));
  });

  it('Renders a team card', function () {
    expect(document.body.innerHTML.includes("FSV Mainz 05"));
  });
});
