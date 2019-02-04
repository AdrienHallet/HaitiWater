L.drawLocal = {
      draw: {
        toolbar: {
          // #TODO: this should be reorganized where actions are nested in actions
          // ex: actions.undo  or actions.cancel
          actions: {
            title: 'Cancel - your text-',
            text: '- your text-'
          },
          finish: {
            title: '- your text-',
            text: '- your text-'
          },
          undo: {
            title: '- your text-',
            text: '- your text-'
          },
          buttons: {
            polyline: '- your text-',
            polygon: '- your text-',
            rectangle: '- your text-',
            circle: '- your text-',
            marker: '- your text-',
            circlemarker: '- your text-'
          }
        },
        handlers: {
          circle: {
            tooltip: {
              start: '- your text-'
            },
            radius: '- your text-'
          },
          circlemarker: {
            tooltip: {
              start: '- your text-.'
            }
          },
          marker: {
            tooltip: {
              start: '- your text-.'
            }
          },
          polygon: {
            tooltip: {
              start: '- your text-.',
              cont: '- your text-.',
              end: '- your text-.'
            }
          },
          polyline: {
            error: '<strong>Erreur:</strong> les lignes ne peuvent se croiser !',
            tooltip: {
              start: 'Cliquez pour commencer la ligne',
              cont: 'Cliquez pour continuer la ligne.',
              end: 'Cliquez le dernier point pour terminer.'
            }
          },
          rectangle: {
            tooltip: {
              start: '- your text-.'
            }
          },
          simpleshape: {
            tooltip: {
              end: 'Release mouse to finish drawing.'
            }
          }
        }
      },
      edit: {
        toolbar: {
          actions: {
            save: {
              title: 'Save changes',
              text: 'Save'
            },
            cancel: {
              title: 'Cancel editing, discards all changes',
              text: 'Cancel'
            },
            clearAll: {
              title: 'Clear all layers',
              text: 'Clear All'
            }
          },
          buttons: {
            edit: 'Edit layers',
            editDisabled: 'No layers to edit',
            remove: 'Delete layers',
            removeDisabled: 'No layers to delete'
          }
        },
        handlers: {
          edit: {
            tooltip: {
              text: 'Drag handles or markers to edit features.',
              subtext: 'Click cancel to undo changes.'
            }
          },
          remove: {
            tooltip: {
              text: 'Click on a feature to remove.'
            }
          }
        }
      }
    };
