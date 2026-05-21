-- Pandoc Lua过滤器：保留LaTeX公式为文本
function Math(elem)
  -- 将数学公式保留为文本，并添加特殊标记
  local formula_text = pandoc.utils.stringify(elem.text)
  local marker = pandoc.RawInline("openxml", '<w:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:sz w:val="24"/></w:rPr><w:t>' .. formula_text .. '</w:t></w:r>')
  return pandoc.Span({marker})
end

function display_math(elem)
  -- 显示公式（块级）
  local formula_text = pandoc.utils.stringify(elem.text)
  return pandoc.Para({
    pandoc.RawInline("openxml", '<w:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:b w:val="1"/></w:rPr><w:t>公式: ' .. formula_text .. '</w:t></w:r>')
  })
end

return {{Math = Math, DisplayMath = display_math}}
