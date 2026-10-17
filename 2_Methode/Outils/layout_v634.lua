-- Pagination de la synthèse : groupes cohérents, tableaux courts intacts.
function Header(el)
  local text = pandoc.utils.stringify(el.content)
  if text:match('^Racines recoupées') or text:match('^4%. Le lemme') or text:match('^5%. Prochaines') then
    return {pandoc.RawBlock('latex', '\\newpage'), el}
  end
end
