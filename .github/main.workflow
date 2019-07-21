workflow "Build" {
  on = "push"
  resolves = [
    "Lint",
  ]
}

action "Install" {
  args = "pip install --upgrade pip && pip install black pylint pydocstyle"
  uses = "jefftriplett/python-actions@master"
}

action "Lint" {
  args = "black . --verbose && pydocstyle . --verbose && pylint thermometer -d C0330 --verbose"
  uses = "jefftriplett/python-actions@master"
  needs = ["Install"]
}