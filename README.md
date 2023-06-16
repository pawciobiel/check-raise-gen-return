# check-raise-gen-return

This is [pre-commit](https://pre-commit.com/) hook
that will check if your code contains `raise gen.Return` _or similar_.

It is only useful if you use [tornado](https://www.tornadoweb.org/) web framework 
with python >=3.3 and want to refactor your code to use `return` as opposed to `raise gen.Return`

See docs for more info: https://www.tornadoweb.org/en/stable/gen.html#tornado.gen.Return

The simplest way to remove most `gen.Return` occurrences may be to use something similar to this:
```
git grep -l 'raise gen.Return' | xargs sed -i -E 's|raise gen.Return\(([]{}[[:print:]]+)(\)$)|return \1|'
```

### Usage

Install [pre-commit](https://pre-commit.com/)


and add this to your .pre-commit-config.yaml:

```
- repo: https://github.com/pawciobiel/check-raise-gen-return
  rev: v0.0.1
  hooks:
    - id: check-raise-gen-return
```
