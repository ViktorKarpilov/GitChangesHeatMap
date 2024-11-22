function CreateGitStat{

    # Get all changed files and process them in one go
    $fileChanges = (git log --pretty="format:" --name-only | Where-Object { $_ })

    # Group and count files by their base name
    $results = $fileChanges
      | Group-Object
      | Where-Object { $_.Count -gt 1 }
      | Select-Object @{ Name = 'Count'; Expression = { $_.Count } }, @{ Name = 'File'; Expression = { $_.Name } }

    $results | Export-Csv "heatmap-data.csv" -NoTypeInformation
}
