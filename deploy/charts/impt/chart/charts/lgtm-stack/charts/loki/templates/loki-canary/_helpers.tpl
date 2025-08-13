{{/*
canary fullname
*/}}
{{- define "loki-canary.fullname" -}}
{{ include "loki.name" . }}-canary
{{- end }}

{{/*
canary common labels
*/}}
{{- define "loki-canary.labels" -}}
{{ include "loki.labels" . }}
app.kubernetes.io/component: canary
{{- end }}

{{/*
canary selector labels
*/}}
{{- define "loki-canary.selectorLabels" -}}
{{ include "loki.selectorLabels" . }}
app.kubernetes.io/component: canary
{{- end }}

{{/*
canry priority class name
*/}}
{{- define "loki-canary.priorityClassName" -}}
{{- $pcn := coalesce .Values.global.priorityClassName .Values.read.priorityClassName -}}
{{- if $pcn }}
priorityClassName: {{ $pcn }}
{{- end }}
{{- end }}
